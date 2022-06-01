import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SaltComponent } from './salt.component';

describe('SaltComponent', () => {
  let component: SaltComponent;
  let fixture: ComponentFixture<SaltComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SaltComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SaltComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
